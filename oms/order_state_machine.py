from __future__ import annotations

from oms.order_state import OrderState


class OrderStateMachine:

    VALID_TRANSITIONS = {

        OrderState.CREATED: {
            OrderState.PENDING_SUBMIT,
            OrderState.REJECTED,
        },

        OrderState.PENDING_SUBMIT: {
            OrderState.SUBMITTED,
            OrderState.REJECTED,
            OrderState.FAILED,
        },

        OrderState.SUBMITTED: {
            OrderState.ACKNOWLEDGED,
            OrderState.REJECTED,
            OrderState.CANCEL_PENDING,
        },

        OrderState.ACKNOWLEDGED: {
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.CANCEL_PENDING,
        },

        OrderState.PARTIALLY_FILLED: {
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.CANCEL_PENDING,
        },

        OrderState.CANCEL_PENDING: {
            OrderState.CANCELLED,
        },
    }

    def can_transition(
        self,
        current: OrderState,
        target: OrderState,
    ):

        return target in self.VALID_TRANSITIONS.get(
            current,
            set(),
        )