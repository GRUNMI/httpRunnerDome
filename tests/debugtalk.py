def get_postids(num):
    postid = 350757819118
    postid_list = []
    for i in range(num):
        postid += 1
        postid_list.append({"postid2": str(postid)})
    return postid_list

def get_post_id():
    return [
        {
            "type1": "huitongkuaidi",
            "postid2": "350757819119"
        }
    ]

if __name__ == '__main__':
    post_list = get_postids(5)
    print(post_list)
