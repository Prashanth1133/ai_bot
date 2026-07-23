class EarlyStopping:



    def __init__(

        self,

        patience=25,

        minimum_loss=0.001

    ):


        self.best_loss = None

        self.counter = 0

        self.patience = patience

        self.minimum_loss = minimum_loss


    def stop(

        self,
        loss

    ):


        if self.best_loss is None:


            self.best_loss = loss

            return False


        if loss < self.best_loss:


            self.best_loss = loss

            self.counter = 0

            return False


        self.counter +=1


        if self.counter >= self.patience:


            return True


        if loss <= self.minimum_loss:


            return True


        return False