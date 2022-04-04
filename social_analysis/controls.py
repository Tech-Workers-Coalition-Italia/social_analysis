def get_histnorm_from_measure_type(measure_type):
    assert measure_type in ('Valore Assoluto', 'Valore Relativo'), f"Invalid measure_type value {measure_type}"
    return "probability" if measure_type == 'Valore Relativo' else None