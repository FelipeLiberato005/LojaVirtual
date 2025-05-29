-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS loja_virtual;
USE loja_virtual;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    estoque INT NOT NULL,
    imagem_url VARCHAR(255)
);

-- Tabela de endereços
CREATE TABLE IF NOT EXISTS endereco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    endereco VARCHAR(255) NOT NULL, 
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL, 
    cep VARCHAR(20) NOT NULL, 
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabela de cartões
CREATE TABLE IF NOT EXISTS cartoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    numero_cartao VARCHAR(20) NOT NULL,
    nome_titular VARCHAR(100) NOT NULL,
    validade DATE NOT NULL,
    cvv VARCHAR(4) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabela de compras
CREATE TABLE IF NOT EXISTS compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Exemplo de inserções (teste de dados)

-- Usuário com senha fictícia hashada (gerada por bcrypt no app)
INSERT INTO usuarios (nome, email, senha)
VALUES ('felipe22', 'felipe22@gmail.com', '$2b$12$ExemploHashDaSenha1234567890123456789012');

-- Produtos
INSERT INTO produtos (nome_produto, descricao, preco, categoria, estoque, imagem_url)
VALUES
('Relógio', 'Relógio banhado a ouro', 650.90, 'Acessórios', 5, 'imagens/relogio.jpg'),
('Camisa', 'De algodão, disponível em várias cores e tamanhos', 25.00, 'Roupas', 100, 'static/foto_site/camisa.jpg'),
('Boné', 'De pano, disponível em várias cores', 55.00, 'Roupas', 100, 'imagens/bone.jpeg');

-- Endereço
INSERT INTO endereco (usuario_id, endereco, cidade, estado, cep)
VALUES (1, 'Fenda do Bikini', 'Cidade das Conchas', 'Fenda da Pedra', '90000-000');

-- Cartão
INSERT INTO cartoes (usuario_id, numero_cartao, nome_titular, validade, cvv)
VALUES (1, '1234567890123456', 'Felipe da Silva', '2026-12-01', '123');

-- Compra
INSERT INTO compras (usuario_id, produto_id, quantidade, data_compra)
VALUES (1, 1, 2, NOW());

INSERT INTO usuarios (nome, email, senha, is_admin)
VALUES ('Admin', 'admin@loja.com', '$2b$12$4vY8iFr835K6IoPAPmUMHO/sstl34GVVSLmd4ctsR4.Dnz1oYjtW2', TRUE);

ALTER TABLE usuarios ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;

SELECT * from Usuarios;
DESC usuarios;