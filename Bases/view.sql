 CREATE VIEW PagamentosPorPix AS
SELECT * FROM Pagamento
WHERE MetodoPagamento = 'Pix';

CREATE VIEW PagamentosPorBoleto AS
SELECT * FROM Pagamento
WHERE MetodoPagamento = 'Boleto Bancário';

CREATE VIEW PagamentosPorCartao AS
SELECT * FROM Pagamento
WHERE MetodoPagamento = 'Cartão de Crédito ou Débito';
