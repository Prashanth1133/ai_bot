from evaluation.production_report import (
    ProductionReport
)


result = {

    "accuracy":0.95,

    "mean_error":0.01,

    "confidence":0.93

}


ProductionReport().generate(

    result

)