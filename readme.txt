#Project Title and Introduction
ST_WORK
This project is primarily built for handling STS and TTS work of Lord

#Table of contents
1. Introduction
We have various modules designed for specific use cases and the main focus is on STS and TTS works

2. Installation 
git init
git config --global user.name "Swamiseva"
git config --global user.email "shridattaswamiseva@gmail.com"
git clone https://github.com/Swamiseva/st_work.git

3. Usage
To ignore a specific file to be untracked
    add the file name to .gitignore
    add commit and push it
To push your changes to the repository
    git status
    git add -f * (to add all files use *)
    git commit -m "commit message"
    git push
        username = Swamiseva
        pwd = Personal Access Token
To check the whisper modules
    cd ~/.cache/whisper


4. Features
a. Split the video - with and without compression
b. Convert video to audio

5. Requirements
Run the below command to install all the requirements -->
    pip install -r requirements.txt
Install ffmpeg (on cmd)
    a. Go to https://www.gyan.dev/ffmpeg/builds/
    b. select in master build ffmpeg-git-full.7z
    c. Download it, extract it, and note the path of bin folder which contains ffmpeg.exe. ex - "C:\ffmpeg\ffmpeg-2024-09-26-git-f43916e217-full_build\bin"
    d. Add it to path (environment vairable) either manually or using cmd command. Via this command in cmd-> 
        {setx /m PATH "C:\ffmpeg\ffmpeg-2024-09-26-git-f43916e217-full_build\bin\;%PATH%"}
    e. Restart your pc and execute "where ffmpeg" to validate the path of ffmpeg (indicator of Installation)
Install ffmpeg (on WSL)
    sudo apt install ffmpeg (needs additional 250 MB)

6. Additional tools used
https://gotranscript.com/text-compare#diff -> To check accuracy of original text and model output

7. Contact
Swami