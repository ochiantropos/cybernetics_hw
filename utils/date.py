def intersects(start_date1, end_date1, start_date2, end_date2):
    return (start_date1 <= end_date2) and (start_date2 <= end_date1)
