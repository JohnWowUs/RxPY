from rx.observable import Observable
from rx.internal import extends


@extends(Observable)
class ToFuture(object):

    def to_future(self, future_ctor=None):
        """Converts an existing observable sequence to a Future

        Example:
        future = rx.Observable.return(42).to_future(RSVP.Promise);

        With config:
        Rx.config.Promise = RSVP.Promise
        promise = rx.Observable.return(42).to_future()

        future_ctor -- {Function} [Optional] The constructor of the future.
            If not provided, it looks for it in rx.config.Future.

        Returns {Future} An future with the last value from the observable
        sequence.
        """

        future_ctor = future_ctor or rx.config.get("Future")
        if not future_ctor:
            raise Exception('Future type not provided nor in rx.config.Future')

        source = self

        future = future_ctor()

        value = [None]
        has_value = [False]

        def on_next(v):
            value[0] = v
            has_value[0] = True

        def on_error(err):
            future.set_exception(err)

        def on_completed():
            if has_value[0]:
                future.set_result(value[0])

        source.subscribe(on_next, on_error, on_completed)

        # No cancellation can be done
        return future
