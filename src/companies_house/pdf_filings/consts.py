def init_fields():
    directors = []

    current_cash = []
    prev_cash = []

    current_total_revenue = []
    prev_total_revenue = []

    current_total_turnover = []
    previous_total_turnover = []

    current_uk_revenue = []
    previous_uk_revenue = []

    current_uk_turnover = []
    previous_uk_turnover = []

    possible_cash_pages = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

    possible_total_revenue_pages = [5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    possible_revenue_pages = [14, 15, 16, 17, 18, 19, 28]
    return (
        directors,
        current_cash,
        prev_cash,
        current_total_revenue,
        prev_total_revenue,
        current_total_turnover,
        previous_total_turnover,
        current_uk_revenue,
        previous_uk_revenue,
        current_uk_turnover,
        previous_uk_turnover,
        possible_cash_pages,
        possible_total_revenue_pages,
        possible_revenue_pages,
    )


def get_list_of_coordinates(coords):
    return [
        coords - 5,
        coords - 4,
        coords - 3,
        coords - 2,
        coords - 1,
        coords,
        coords + 1,
        coords + 2,
        coords + 3,
        coords + 4,
        coords + 5,
    ]
