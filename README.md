# Free World Certified

## Welcome

This monorepo contains the application and website for
freeworldcertified.org

## Installation

### Clone or Download

- Clone this repo to your local machine using

```bash
git clone https://github.com/freeworldcertified/fwc.git
```

### Required to install

- For running the container, you need to add your own .env file inside ./backend/ folder.
- More details are inside the ./backend/README.md file in "Environment" section.

### How to run locally

- Start the terminal.
- Run the following command
- Open your browser to <http://localhost:3000/> for the fwc website
- Open your browser to <http://localhost:3001/> for access to the mock email server to setup accounts

```bash
docker-compose up --build
```

### Pre-commit feature

- Follow sections "Create a virtual environment" and "Required to install" in the README.md file inside
  ./backend folder.
- Run the following command:

```bash
pre-commit install
```

### To run the end-to-end tests

- Run this command from project directory:

```bash
docker-compose -f docker-compose.test.yaml up --abort-on-container-exit --build
```

### Node version

- node version 12.x does not work. node 16.x does work. other node versions may work we have not confirmed.
- Use this command to check your version:

```bash
node -v
```

- If it fails, consider running [nvm](https://github.com/nvm-sh/nvm), and using that to run
  version 16 or above.

### Github Actions / Workflows

- These can be tested using the [act](https://github.com/nektos/act) tool
- Ubuntu installation can be found [here](https://lindevs.com/install-act-on-ubuntu)

```bash
wget -qO act.tar.gz https://github.com/nektos/act/releases/latest/download/act_Linux_x86_64.tar.gz
sudo tar xf act.tar.gz -C /usr/local/bin act
act --version
```
