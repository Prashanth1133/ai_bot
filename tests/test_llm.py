from ai.llm_engine import LLMEngine


result = (

    LLMEngine().reasoning(

        {

            "news":"BULLISH",

            "whale":"BULLISH",

            "liquidation":"BULLISH",

            "options":"BULLISH",

            "signal":"BUY"

        }

    )

)


print(result)