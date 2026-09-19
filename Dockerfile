FROM nvidia/cuda:12.9.2-devel-ubuntu24.04

RUN apt update && apt install -y wget git

WORKDIR /boost
RUN wget https://archives.boost.io/release/1.84.0/source/boost_1_84_0.tar.bz2
RUN tar xf boost_1_84_0.tar.bz2
WORKDIR /boost/boost_1_84_0
RUN ./bootstrap.sh --prefix=/usr/local
RUN ./b2
RUN ./b2 install
RUN echo "LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> /etc/bash.bashrc

WORKDIR /vina
RUN git clone https://github.com/DeltaGroupNJUPT/Vina-GPU-2.1.git /vina
WORKDIR /vina/AutoDock-Vina-GPU-2.1
RUN apt update && apt install -y ocl-icd-opencl-dev
RUN sed -i "s|WORK_DIR=.*|WORK_DIR=/vina/AutoDock-Vina-GPU-2.1|" Makefile
RUN sed -i "s|BOOST_LIB_PATH=.*|BOOST_LIB_PATH=/boost/boost_1_84_0|" Makefile
RUN make clean
RUN make source
