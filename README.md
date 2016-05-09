# putty2openssh
Converting PuTTY saved sessions to openssh .ssh/config file format

## Input
On Windows:

`reg export HKCU\Software\SimonTatham putty.reg /y`

Copy the generate reg file to a linux/osx machine
Depending on the source system (mine is Windows 8.1) you might need to
convert the charset:

`iconv -f utf-16le -t utf-8 < ./putty.reg > ./putty-utf8.reg`

Remove the first line (everything before the first [...] section header

## RUN

`python parse.py >> ~/.ssh/config`

It needs a lot of improvement obviously but I needed this very quickly so
it's quick 'n dirty.

PR's are welcome

## PPK key files to openssh formats

Dirty mass convert:

`for i in *.ppk; do base=${i%.*}; echo "Converting $i ..." ; puttygen $i -O private-openssh -o ~/.ssh/$base.pem ; done`

On OSX you can install puttygen with `brew install putty` given that you have brew already.

On Ubuntu you can install puttygen with `apt-get install putty`

You might need to `chmod 600 ~/.ssh/*.pem`
