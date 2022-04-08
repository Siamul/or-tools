FROM ortools/make:ubuntu_base AS env
RUN make -version

FROM env AS devel
WORKDIR /home/project
COPY . .

FROM devel AS build
RUN make third_party BUILD_DOTNET=OFF BUILD_JAVA=OFF BUILD_PYTHON=OFF
RUN make cpp

FROM build AS test
RUN make test_cpp

FROM build AS package
RUN make package_cpp
