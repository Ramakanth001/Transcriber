# Transcriber - Speech-to-Text (STS) Work

**Transcriber** is a project focused on handling Speech-to-Text (STS) and Text-to-Speech (TTS) tasks with a suite of modules designed for these specific use cases. This repository aims to provide high-quality, seamless STS and TTS solutions. The main emphasis is on enabling efficient audio-visual conversions and manipulation.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Requirements](#requirements)
6. [Additional Tools](#additional-tools)
7. [Contact](#contact)

---

## Introduction

The **Transcriber** project includes a variety of modules, with the core functionality centered around Speech-to-Text (STS) and Text-to-Speech (TTS) operations. The project is designed to support both the transcription of speech into text and the conversion of text into synthesized speech, offering the flexibility to manipulate audio and video files.

Key functionalities include:
- Speech-to-text (STS) conversion
- Text-to-speech (TTS) conversion - in_progress
- Video splitting (with and without compression)
- Video-to-audio conversion

---

## Installation

To get started with **Transcriber**, follow these steps:

### Step 1: Initialize a Git Repository

```bash
git init
git config --global user.name "Swamiseva"
git config --global user.email "shridattaswamiseva@gmail.com"
git clone https://github.com/Swamiseva/Transcriber.git
```

---

## Usage

Here’s a guide on how to use the basic functionalities of the project:

### Push a Specific File

Add the file, Commit and push your changes:

```bash
git status
git add -f *  # To add all files
git commit -m "commit message"
git push
```

*Note:* You will need to enter your GitHub username and Personal Access Token for authentication.

### Whisper Modules

To check the whisper modules, navigate to the following directory:

```bash
cd ~/.cache/whisper
```
---

**Note:** You free to you any model size of your choice - Tiny, small, medium, large, turbo. Condider the tradeoffs of speed, accuracy and model size accordingly. By default we would be using the medium model


## Features

Here are the primary features of the **Transcriber** project:

### a. Split the Video
- Split videos both **with** and **without** compression.

### b. Convert Video to Audio
- Extract the audio from video files, enabling you to process and manipulate the audio.

---

## Requirements

Ensure that you have all the necessary dependencies installed. You can install them by running:

```bash
pip install -r requirements.txt
```

### FFmpeg Installation

**FFmpeg** is required for video and audio processing.

#### On Windows:
1. Go to [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/).
2. Select the master build `ffmpeg-git-full.7z`.
3. Download, extract it, and note the path to the `bin` folder that contains `ffmpeg.exe` (e.g., `C:\ffmpeg\ffmpeg-2024-09-26-git-full_build\bin`).
4. Add this path to your environment variables (system path):

   ```bash
   setx /m PATH "C:\ffmpeg\ffmpeg-2024-09-26-git-f43916e217-full_build\bin\;%PATH%"
   ```

5. Restart your PC and verify FFmpeg installation by running:

   ```bash
   where ffmpeg
   ```

#### On WSL (Windows Subsystem for Linux):
```bash
sudo apt install ffmpeg
```

Note: WSL requires an additional 250 MB of space.

---

## Additional Tools

For accuracy comparison between original text and model output, use the [Text Compare Tool](https://gotranscript.com/text-compare#diff).

---

## Contact

For any inquiries or issues related to the project, feel free to contact:

**Ramakanth**  
Email: [ramakanthseshabhattar@gmail.com](mailto:ramakanthseshabhattar@gmail.com)  

---


Thank you for exploring **Transcriber**! 🌟

---

<div align="center">

_A powerful tool for efficient STS and TTS conversion._

</div>

---
