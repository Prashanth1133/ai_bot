import torch


class ColabTrainer:


    def information(self):


        print("\n")


        print(

            "CUDA :",torch.cuda.is_available()

        )


        if torch.cuda.is_available():

            print(

                "GPU :",

                torch.cuda.get_device_name(0)

            )


        print("\n")