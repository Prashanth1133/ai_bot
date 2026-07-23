import torch


class ProductionValidator:


    @torch.no_grad()

    def validate(

        self,
        model,
        loader

    ):


        model.eval()

        batches = 0


        for _,_ in loader:

            batches +=1


        model.train()


        return {

            "validation_batches":

            batches

        }