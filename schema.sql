CREATE TABLE IF NOT EXISTS usuaris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuari VARCHAR(80) NOT NULL UNIQUE,
    contrasenya VARCHAR(255) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS jocs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(120) NOT NULL UNIQUE,
    actiu TINYINT(1) NOT NULL DEFAULT 1
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

create table if not exists partides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    joc_nom VARCHAR(120) NOT NULL,
    puntuacio INT NOT NULL,
    data_hora DATETIME NOT NULL,
    errors INT NOT NULL DEFAULT 0
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

INSERT INTO
    jocs (nom, actiu)
VALUES ('Flux de Paraules', 1),
    ('Neon Drift', 1),
    ('Seleccio en orde', 1);
