import inspect
from datatable_operations import DataTableOperations

class Game:
    def __init__(
            self,
            game_id,
            name,
            favorite,
        ):
        self.game_id = game_id,
        self.name = name,
        self.favorite = favorite,
        
    dto = DataTableOperations()
        
    def get_name(self, name):
        print(inspect.currentframe().f_code.co_name)
        return name
        
    def get_favorite(self, favorite_icon):
        print(inspect.currentframe().f_code.co_name)
        if favorite_icon == "star":
            return 1
        else:
            return 0
    
    def get_counting_method(self, counting_method):
        print(inspect.currentframe().f_code.co_name)
        return counting_method
        
    def get_game_end_condition(self, game_end_condition):
        print(inspect.currentframe().f_code.co_name)
        return game_end_condition

    def get_points_on_start(self, points_on_start):
        print(inspect.currentframe().f_code.co_name)
        return points_on_start

    def get_score_ending_the_game(self, score_ending_the_game):
        print(inspect.currentframe().f_code.co_name)
        return score_ending_the_game

    def get_number_of_rounds(self, number_of_rounds):
        print(inspect.currentframe().f_code.co_name)
        return number_of_rounds

    def get_round_name(self, round_name):
        print(inspect.currentframe().f_code.co_name)
        return round_name
        
    def get_rounds(self, table_name):
        print(inspect.currentframe().f_code.co_name)
        return self.dto.get_rows_from_table(table_name)
 
class CountingMethod:
    def __init__(
            self,
            counting_method_id,
            name,
            game_id,
            scoring_type_rivcoop,
            scoring_type_highlow,
            scoring_type_updown,
            scoring_type_endround,
            scoring_type_defrounds,
            game_end_condition,
            points_on_start,
            score_ending_the_game,
            number_of_rounds,
            round_name,
        ):
        self.counting_method_id = counting_method_id,
        self.name = name,
        self.game_id = game_id,
        self.scoring_type_rivcoop = scoring_type_rivcoop,
        self.scoring_type_highlow = scoring_type_highlow,
        self.scoring_type_updown = scoring_type_updown,
        self.scoring_type_endround = scoring_type_endround,
        self.scoring_type_defrounds = scoring_type_defrounds,
        self.game_end_condition = game_end_condition,
        self.points_on_start = points_on_start,
        self.score_ending_the_game = score_ending_the_game,
        self.number_of_rounds = number_of_rounds,
        self.round_name = round_name,

class Round:
    def __init__(
            self,
            round_id,
            name,
            order_no,
            game_id
            ):
        self.round_id = round_id,
        self.name = name,
        self.order_no = order_no,
        self.game_id = game_id,

class Category:
    def __init__(
            self,
            category_id,
            name,
            order_no,
            game_id
            ):
        self.category_id = category_id,
        self.name = name,
        self.order_no = order_no,
        self.game_id = game_id,
                        