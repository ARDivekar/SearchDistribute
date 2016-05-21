class SearchConfig:

    def __init__(self, query=None, num_pages=1, num_results_per_page=10, in_url=None, in_title=None, file_type=None):
        self.query = query
        self.num_pages = num_pages
        self.num_results_per_page = num_results_per_page
        self.in_url = in_url
        self.in_title = in_title
        self.file_type = file_type
