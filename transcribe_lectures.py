#!/usr/bin/env python3

import argparse
import json
import time
from pathlib import Path

import mlx_whisper


SUPPORTED_AUDIO_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".mp4",
    ".wav",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch-transcribe lecture audio files with mlx-whisper."
    )
    parser.add_argument(
        "--input-dir",
        default="audio",
        help="Directory containing audio files to transcribe.",
    )
    parser.add_argument(
        "--output-dir",
        default="transcripts",
        help="Directory where transcript files will be written.",
    )
    parser.add_argument(
        "--model",
        default="mlx-community/whisper-small",
        help="MLX Whisper model repo or local path.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Optional language code such as 'en'. Defaults to auto-detect.",
    )
    parser.add_argument(
        "--word-timestamps",
        action="store_true",
        help="Include word-level timestamps in the JSON output.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files whose .txt and .json outputs already exist.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only process the first N audio files.",
    )
    parser.add_argument(
        "--clip-timestamps",
        default="0",
        help="Optional Whisper clip timestamps string, for example '0,60' for a 60-second smoke test.",
    )
    return parser.parse_args()


def find_audio_files(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    )


def transcript_text(result: dict) -> str:
    lines = []
    for segment in result.get("segments", []):
        text = segment.get("text", "").strip()
        if text:
            lines.append(text)
    return "\n".join(lines).strip() + "\n"


def write_outputs(result: dict, output_base: Path) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    output_base.with_suffix(".txt").write_text(
        transcript_text(result),
        encoding="utf-8",
    )
    output_base.with_suffix(".json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    audio_files = find_audio_files(input_dir)
    if args.limit is not None:
        audio_files = audio_files[: args.limit]

    if not audio_files:
        raise SystemExit("No supported audio files found.")

    summary: list[dict] = []
    successes = 0
    skipped = 0
    failures = 0

    for index, audio_file in enumerate(audio_files, start=1):
        output_base = output_dir / audio_file.stem
        txt_path = output_base.with_suffix(".txt")
        json_path = output_base.with_suffix(".json")

        if args.skip_existing and txt_path.exists() and json_path.exists():
            print(f"[{index}/{len(audio_files)}] SKIP {audio_file.name}")
            skipped += 1
            summary.append(
                {
                    "audio_file": audio_file.name,
                    "status": "skipped",
                    "txt_path": str(txt_path),
                    "json_path": str(json_path),
                }
            )
            continue

        print(f"[{index}/{len(audio_files)}] START {audio_file.name}")
        started_at = time.perf_counter()

        try:
            result = mlx_whisper.transcribe(
                str(audio_file),
                path_or_hf_repo=args.model,
                verbose=False,
                language=args.language,
                word_timestamps=args.word_timestamps,
                clip_timestamps=args.clip_timestamps,
            )
            write_outputs(result, output_base)
            elapsed = time.perf_counter() - started_at
            print(f"[{index}/{len(audio_files)}] OK    {audio_file.name} ({elapsed:.1f}s)")
            successes += 1
            summary.append(
                {
                    "audio_file": audio_file.name,
                    "status": "ok",
                    "language": result.get("language"),
                    "elapsed_seconds": round(elapsed, 2),
                    "txt_path": str(txt_path),
                    "json_path": str(json_path),
                }
            )
        except Exception as exc:  # noqa: BLE001
            elapsed = time.perf_counter() - started_at
            print(f"[{index}/{len(audio_files)}] FAIL  {audio_file.name} ({elapsed:.1f}s) - {exc}")
            failures += 1
            summary.append(
                {
                    "audio_file": audio_file.name,
                    "status": "failed",
                    "elapsed_seconds": round(elapsed, 2),
                    "error": str(exc),
                }
            )

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "model": args.model,
                "language": args.language,
                "word_timestamps": args.word_timestamps,
                "clip_timestamps": args.clip_timestamps,
                "input_dir": str(input_dir),
                "output_dir": str(output_dir),
                "successes": successes,
                "skipped": skipped,
                "failures": failures,
                "files": summary,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Summary: {successes} succeeded, {skipped} skipped, {failures} failed. "
        f"Details: {summary_path}"
    )
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
