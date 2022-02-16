class ChessBoard:
    def __init__(self) -> None:
        self.Board=[
            ["BR1","BN1","BB1","BQ","BK","BB2","BN2","BR2"],
            ["BP1","BP2","BP3","BP4","BP5","BP6","BP7","BP8"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["WP1","WP2","WP3","WP4","WP5","WP6","WP7","WP8"],
            ["WR1","WN1","WB1","WQ","WK","WB2","WN2","WR2"] 
        ]
        self.black_turn=False
        self.white_turn=True
    
    def move(self,piece_name):
        # move conditions for each peice
        print("Invalid")
    
    
