FROM haskell:latest

WORKDIR /workspaces/haskell-server-app

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt update \
    && apt install -y --no-install-recommends sudo \
    && echo $USERNAME ALL=\(ALL\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME 

USER $USERNAME

ENV PATH="/home/$USERNAME/.cabal/bin:/home/$USERNAME/.local/bin:$PATH"
