def trans_time(duration: int):
    hour = int(duration // 3600)
    minute = int(duration // 60 % 60)
    second = int(duration % 60)
    return f"{f'{hour}:' if hour else ''}{minute}:{second}"
