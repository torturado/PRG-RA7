# Deployment en Proxmox LXC con Docker

Guia per desplegar el projecte des de zero en un contenidor LXC de Proxmox utilitzant Docker i Docker Compose.

## 1. Preparar el LXC

Des del host Proxmox, activa les funcionalitats necessaries per executar Docker dins del LXC:

```bash
pct set ID_DEL_LXC -features nesting=1,keyctl=1
pct restart ID_DEL_LXC
```

Despres entra al LXC com a `root`.

## 2. Instal-lar Docker

```bash
apt update
apt install -y ca-certificates curl

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

printf '%s\n' \
'Types: deb' \
'URIs: https://download.docker.com/linux/debian' \
"Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")" \
'Components: stable' \
"Architectures: $(dpkg --print-architecture)" \
'Signed-By: /etc/apt/keyrings/docker.asc' \
> /etc/apt/sources.list.d/docker.sources

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable --now docker
```

Comprova la instal-lacio:

```bash
docker --version
docker compose version
```

## 3. Descarregar el projecte

```bash
git clone https://github.com/torturado/PRG-RA7.git
cd PRG-RA7
```

Si el projecte ja existeix al servidor:

```bash
cd PRG-RA7
git pull
```

## 4. Configurar variables d'entorn

Copia el fitxer d'exemple:

```bash
cp .env.example .env
```

Edita `.env` i canvia `SECRET_KEY` per una clau llarga i aleatoria:

```bash
nano .env
```

Exemple:

```env
DB_HOST=mariadb
DB_PORT=3306
DB_USER=icgames_user
DB_PASSWORD=icgames1234
DB_NAME=icgames
MONGODB_URL=mongodb://root:changeme@mongodb:27017/projecte_prg?authSource=admin
SECRET_KEY=una_clave_larga_y_aleatoria
```

## 5. Aixecar l'aplicacio

```bash
docker compose up -d --build
```

Comprova l'estat dels contenidors:

```bash
docker compose ps
```

Veure logs de Flask:

```bash
docker compose logs -f web
```

## 6. Accedir a l'aplicacio

Obre al navegador:

```text
http://IP_DEL_LXC:5000
```

Exemple:

```text
http://192.168.1.50:5000
```

## 7. Comandes utils

Parar els serveis:

```bash
docker compose down
```

Reiniciar els serveis:

```bash
docker compose restart
```

Actualitzar des de GitHub:

```bash
git pull
docker compose up -d --build
```

Veure tots els logs:

```bash
docker compose logs -f
```

Veure logs nomes de Flask:

```bash
docker compose logs -f web
```

## 8. Serveis desplegats

El deployment aixeca aquests serveis:

- `web`: aplicacio Flask servida amb Gunicorn.
- `mariadb`: base de dades MariaDB amb l'esquema inicial.
- `mongodb`: base de dades MongoDB per guardar l'historic de partides.
- Volums persistents per conservar les dades de MariaDB i MongoDB.
- Port extern `5000` per accedir a l'aplicacio.

