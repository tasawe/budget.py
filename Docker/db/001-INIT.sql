CREATE TABLE types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(255) NOT NULL
);

CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cat_name VARCHAR(255) NOT NULL
);

CREATE TABLE entries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL,
    type_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categorias(id),
    FOREIGN KEY (type_id) REFERENCES types(id)
);

CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL
)

INSERT INTO types(type_name) VALUES ("receita");
INSERT INTO types(type_name) VALUES ("despesa");

INSERT INTO categorias(cat_name) VALUES ("lazer");
INSERT INTO categorias(cat_name) VALUES ("transporte");