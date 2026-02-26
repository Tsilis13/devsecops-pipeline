FROM ubuntu:24.04

RUN apt update && apt install -fy gcc make git

RUN git clone https://github.com/HewlettPackard/wireless-tools/ && cd wireless-tools/wireless_tools && make
