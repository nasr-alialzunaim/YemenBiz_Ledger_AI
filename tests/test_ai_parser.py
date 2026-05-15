from backend.app.services.ai_parser import NaturalLanguageSaleParser


def test_parse_arabic_credit_sale():
    parser = NaturalLanguageSaleParser()
    result = parser.parse("بعت لأحمد 3 كرتون ماء و2 كيس رز آجل بـ 18500 ريال")

    assert result.payment_type == "credit"
    assert result.total_amount == 18500
    assert result.remaining_amount == 18500
    assert result.items
