FROM ubuntu

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

RUN apt update \
    && apt dist-upgrade -y \
    && apt install -y \
    sudo \
    git \
    python3 \
    python3-pip \
    python3-docutils \
    python3-venv

# Create dev user
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -ms /bin/bash ${USERNAME} \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME} \
    && sed -i 's/\\h/container/g' /home/${USERNAME}/.bashrc \
    && mkdir /command_history \
    && touch /command_history/.bash_history \
    && chown -R ${USERNAME} /command_history \
    && echo "export PROMPT_COMMAND='history -a'" >> "/home/${USERNAME}/.bashrc" \
    && echo "export HISTFILE=/command_history/.bash_history" >> "/home/${USERNAME}/.bashrc" \
    && mkdir /home/${USERNAME}/.vscode-server \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

USER ${USERNAME}

RUN python3 -m pip install bs4 requests build coverage