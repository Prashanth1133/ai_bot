import torch


def gpu_information():


    print("\n")

    print("="*60)

    print("GPU INFORMATION")

    print("="*60)


    print(

        "CUDA Available :",

        torch.cuda.is_available()

    )


    if torch.cuda.is_available():


        print(

            "GPU Name :",

            torch.cuda.get_device_name(

                0

            )

        )


        print(

            "GPU Count :",

            torch.cuda.device_count()

        )


        memory = (

            torch.cuda.get_device_properties(

                0

            ).total_memory

            /(1024**3)

        )


        print(

            "Total Memory :",

            round(

                memory,

                2

            ),

            "GB"

        )


        print(

            "Allocated Memory :",

            round(

                torch.cuda.memory_allocated(

                    0

                )/(1024**3),

                2

            ),

            "GB"

        )


        print(

            "Reserved Memory :",

            round(

                torch.cuda.memory_reserved(

                    0

                )/(1024**3),

                2

            ),

            "GB"

        )


    else:


        print(

            "GPU NOT AVAILABLE."

        )


    print("="*60)

    print("\n")


if __name__ == "__main__":

    gpu_information()