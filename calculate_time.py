import timeit
from py2neo import Graph, Node, Relationship


graph = Graph(password='fighting33')
user_map = {}

def read_file_by_line(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        while True:
            data = f.readline()
            if not data:
                break
            yield data


def insert_rating(node_id, rating, node_movie, graph):
    rel = Relationship(node_id, 'RATINGS', node_movie, rating=rating)
    graph.create(rel)


def main():
    # Can I keep the user_node
    text_generator = read_file_by_line('./ml-10M100K/ratings.dat')
    # for text in text_generator:
    for text in text_generator:
        splitted_text = text.split('::')
        user_id, movie_id, ratings = splitted_text[0:3]
        query = 'match (n:Movie{id:\'%s\'}) return (n)' % movie_id
        movie_node = graph.run(query).data()[0]['n']
        if user_id not in user_map.keys():
            user_node = Node("User", id=user_id)
            user_map[user_id] = user_node
            insert_rating(user_node, ratings, movie_node, graph)
        else:
            user_node = user_map[user_id]
            insert_rating(user_node, ratings, movie_node, graph)


if __name__ == '__main__':
    # 70 ms
    main()