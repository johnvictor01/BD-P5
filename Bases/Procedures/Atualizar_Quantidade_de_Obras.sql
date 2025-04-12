-- Procedimento Para atualizar quantidade de Compras
-- Atualizar SGBD

DELIMITER //

CREATE PROCEDURE AtualizarQuantidadeObrasCompradas(IN matricula VARCHAR(15))
BEGIN
    DECLARE total_vendas INT;
    DECLARE cliente_id INT;

    -- Obtém o PessoaID (ClienteID) correspondente à matrícula
    SELECT PessoaID INTO cliente_id
    FROM Cliente
    WHERE MatriculaCliente = matricula;

    -- Conta o número de vendas feitas pelo cliente
    SELECT COUNT(*) INTO total_vendas
    FROM Venda
    WHERE ClienteID = cliente_id;

    -- Atualiza a quantidade de obras compradas
    UPDATE Cliente
    SET QuantidadeObrasCompradas = total_vendas
    WHERE PessoaID = cliente_id;
END //

DELIMITER ;
