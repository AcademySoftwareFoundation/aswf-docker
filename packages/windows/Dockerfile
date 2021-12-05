
# https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container advises tht dotnet is needed for build tools
FROM mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2019 AS ci-windows-conan

SHELL ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command"]

ARG ASWF_CONAN_VERSION
ARG ASWF_CONAN_PYTHON_VERSION
ENV ASWF_CONAN_VERSION=${ASWF_CONAN_VERSION} \
    ASWF_CONAN_PYTHON_VERSION=${ASWF_CONAN_PYTHON_VERSION}

ENV chocolateyUseWindowsCompression=false \
    PYTHONIOENCODING=UTF-8


RUN iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); \
    $env:Path += '";C:\tools\python3;C:\tools\python3\Scripts"'; \
    choco install --no-progress --yes python3 --version=${Env:ASWF_CONAN_PYTHON_VERSION} --params '"/InstallDir:C:\tools\python3"'

RUN choco install --no-progress --yes visualstudio2017buildtools --version=15.9.41.0
RUN choco install --no-progress --yes visualstudio2017-workload-vctools --version=1.3.1
RUN choco install --no-progress --yes --execution-timeout=0 visualstudio2017-workload-manageddesktop --version=1.2.1

RUN python -m pip install --quiet --upgrade pip; \
    python -m pip install conan==${Env:ASWF_CONAN_VERSION} --quiet --upgrade --force-reinstall --no-cache
    # ; \
#     python -m pip install win-unicode-console --quiet --upgrade --force-reinstall --no-cache; \
#     python -m pip install conan_package_tools --quiet --upgrade --force-reinstall --no-cache

RUN choco install --no-progress --yes cmake --installargs 'ADD_CMAKE_TO_PATH=System'

SHELL ["cmd", "/S", "/C"]
WORKDIR "C:/Users/ContainerAdministrator"
# ENTRYPOINT ["cmd.exe", "C:\\Program Files (x86)\\Microsoft Visual C++ Build Tools\\vcbuildtools_msbuild.bat"]

