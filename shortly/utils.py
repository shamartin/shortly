def create_shortcode(id: int) -> str:
        BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if id == 0:
            return BASE62_CHARS[0]
        encoded_url = []
        num = id
        while num > 0:
           num, remainder = divmod(num, 62)
           encoded_url.append(BASE62_CHARS[remainder])
           
        return "".join(reversed(encoded_url))