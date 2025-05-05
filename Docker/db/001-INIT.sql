CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cat_name VARCHAR(255) NOT NULL
);

CREATE TABLE entries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categorias(id)
);

INSERT INTO categorias(cat_name) VALUES ("receita");
INSERT INTO categorias(cat_name) VALUES ("despesa");