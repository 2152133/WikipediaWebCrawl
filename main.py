def continue_crawl(search_history, target_url):
    if search_history[-1] == target_url:
        return False
    if len(search_history) > 25:
        return False
    i = 0
    while(i < len(search_history)):
        j = i+1
        while(j < len(search_history)):
            if search_history[i] == search_history[j]:
                return False
            j += 1
        i += 1
    return True

