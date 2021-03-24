class Country_data():

    def __init__(self, name, ppp, life_expectancy, urban_percentage, imr, birth_rate, death_rate, tfr, school_years):
        self.name = name
        self.ppp = ppp
        self.life_expectancy = life_expectancy
        self.urban_percentage = urban_percentage
        self.imr = imr
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.tfr = tfr
        self.school_years = school_years
        if not birth_rate == "Data not found." and not death_rate == "Data not found.":
            self.nir = birth_rate - death_rate
        else:
            self.nir = "Data not found."
        self.wins = 0
        self.win_percentage = 0


    def create_positive_stats_list(self):
        stats_list = []
        stats_list.append(self.ppp)
        stats_list.append(self.life_expectancy)
        stats_list.append(self.urban_percentage)
        stats_list.append(self.school_years)
        return stats_list

    def create_negative_stats_list(self):
        stats_list = []
        stats_list.append(self.imr)
        stats_list.append(self.nir)
        stats_list.append(self.tfr)
        return stats_list

    def update_wins(self, opponent):
        my_score = 0
        opponent_score = 0
        my_pos_stats = self.create_positive_stats_list()
        opponent_pos_stats = opponent.create_positive_stats_list()
        for i in range(len(my_pos_stats)):
            if(my_pos_stats[i] == "Data not found."):
                my_pos_stats[i] = -99999999
            if(opponent_pos_stats[i] == "Data not found."):
                opponent_pos_stats[i] = -99999999
            if(my_pos_stats[i] > opponent_pos_stats[i]):
                my_score += 1
            elif(opponent_pos_stats[i] > my_pos_stats[i]):
                opponent_score += 1

        my_neg_stats = self.create_negative_stats_list()
        opponent_neg_stats = opponent.create_negative_stats_list()
        for i in range(len(my_neg_stats)):
            if(my_neg_stats[i] == "Data not found."):
                my_neg_stats[i] = 9999999
            if(opponent_neg_stats[i] == "Data not found."):
                opponent_neg_stats[i] = 9999999
            if(my_neg_stats[i] < opponent_neg_stats[i]):
                my_score += 1
            if(opponent_neg_stats[i] < my_neg_stats[i]):
                opponent_score += 1

        if(my_score > opponent_score):
            self.wins += 1