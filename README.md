# Digital Humanities Intro Lecture

This repository gathers working materials for the University of Bern lecture series `Digital Humanities - Introductions` in `FS 2026`, based on the course program in `Program DH Intro_Online.pdf`.

The lecture series introduces major research areas and methods in Digital Humanities across Swiss universities. According to the program, the course is fully online, the lectures can be watched in any order, and assessment is an open-book multiple-choice exam worth `3 ECTS`.

## Repository Contents

- `Program DH Intro_Online.pdf`: official course program and overview
- `audio/`: local lecture audio files used for transcription
- `videos/`: local lecture video files
- `transcripts/`: full transcript outputs for all 17 lectures
- `transcripts-smoke/`: smoke-test transcription output
- `lecture-overviews/`: one Markdown overview per lecture, based on the transcripts
- `notes-publications/`: lecture-related PDFs and notes
- `transcribe_lectures.py`: batch transcription script using `mlx_whisper`

## Course Logistics

The following points are taken from the program PDF:

- The course is aimed at students across the University of Bern.
- Lectures are provided virtually and can be worked through in any order.
- Two consultation sessions are scheduled for `April 21, 2026` and `May 27, 2026`, both from `12:15` to `14:00`, via Zoom and shared through ILIAS.
- The MC exam takes place on `June 1, 2026`.
- The exam is open book, consists of `20` randomly generated questions, offers `4` possible answers per question, and has no negative marking.
- Students have a `24-hour` window to start the exam and `60 minutes` to complete it once started.

## Lecture Overview

This repo currently contains media and transcripts for all `17` lectures listed in the program.

| Course | Lecturer | Institution | Topic |
| --- | --- | --- | --- |
| 1 | Andreas Fischer | HES-SO & Universitat Fribourg | Text Recognition |
| 2 | Bianca Prietl | Universitat Basel | Understanding Digitalization from Gender Perspectives |
| 3 | Cerstin Mahlow | ZHAW | Digital Linguistics |
| 4 | Elena Chestnova | Universita della Svizzera italiana | Digital Editing: Introduction |
| 5 | Gerhard Lauer | Universitat Mainz | Digital Book Studies |
| 6 | Lukas Rosenthaler | Universitat Basel | Open Linked Data & Semantic Web |
| 7 | Michael Piotrowski | Universite de Lausanne | Theory and Epistemology of Digital Humanities |
| 8 | Noah Bubenhofer | Universitat Zurich | Introduction into Corpus Linguistics |
| 9 | Peter Fornaro | Universitat Basel | Imaging Technologies in DH |
| 10 | Ramona Roller | ETH | Network Analysis |
| 11 | Rico Sennrich | Universitat Zurich & DARIAH | Natural Language Processing |
| 12 | Selena Savic | FHNW | Digitization: Data Materialism in Digital Humanities |
| 13 | Stefan Munnich | Universitat Basel | Digital Musicology |
| 14 | Tobias Hodel | Universitat Bern & DARIAH | Early Modern History after the Machine Learning Turn |
| 15 | Tobias Wildi | FH Graubunden | Introduction to Archives and Digital Preservation |
| 16 | Vera Chiquet | Universitat Basel | Digital Photography |
| 17 | Yannick Rochat | Universite de Lausanne | Game Studies |

## Transcripts

Transcript outputs are stored in `transcripts/` as paired `.txt` and `.json` files. The summary file `transcripts/_summary.json` shows that all `17` lecture audio files were transcribed successfully with the model `mlx-community/whisper-small-mlx`.

Examples:

- `transcripts/Course 1_Fischer_TextRecognition.txt`
- `transcripts/Course 4_Chestnova_DigitalEditing.txt`
- `transcripts/Course 11_Sennrich_NLP.txt`
- `transcripts/Course 15_Wildi_Archives.txt`

## Transcription Script

The script `transcribe_lectures.py` batch-processes files from `audio/` and writes `.txt`, `.json`, and a run summary to an output directory.

Typical usage:

```bash
python3 transcribe_lectures.py --skip-existing
```

Useful options:

- `--input-dir`: source folder, defaults to `audio`
- `--output-dir`: destination folder, defaults to `transcripts`
- `--model`: Whisper model identifier, defaults to `mlx-community/whisper-small`
- `--limit`: process only the first `N` files
- `--clip-timestamps`: useful for smoke tests such as `0,60`
- `--word-timestamps`: include word-level timing in JSON output

## Notes

- Course `9` is marked in the program as `German only` and `not relevant for exam`.
- Further reading lists and links are attached to several lectures in the program PDF and, in some cases, in the lecture slides themselves.
