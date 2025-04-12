-- Procedimento para Atualização de Quantidade Obras Compradas
-- Chamar ao finalizar uma compra

DELIMITER //

CREATE PROCEDURE AtualizarQuantidadeObrasCompradas(IN cliente_id INT)
BEGIN
    DECLARE total_vendas INT;

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
