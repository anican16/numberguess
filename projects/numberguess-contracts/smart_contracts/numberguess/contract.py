import beaker
import pyteal as pt


class Ngstate:
    number = beaker.LocalStateValue(
        stack_type=pt.TealType.bytes, descr="Broj igraca", default=pt.Bytes("Bez broja")
    )
    hash_number = beaker.LocalStateValue(
        stack_type=pt.TealType.bytes,
        descr="Hash broj igraca",
        default=pt.Bytes("Bez hash broja"),
    )
    prvi_igrac = beaker.GlobalStateValue(
        stack_type=pt.TealType.bytes,
        descr="Acc prvog igraca",
        default=pt.Bytes("Bez igraca"),
    )
    drugi_igrac = beaker.GlobalStateValue(
        stack_type=pt.TealType.bytes,
        descr="Acc drugog igraca",
        default=pt.Bytes("Bez igraca"),
    )
    betting_tip = beaker.GlobalStateValue(
        stack_type=pt.TealType.uint64, descr="Betting amount", default=pt.Int(0)
    )


app = beaker.Application("numberguess", state=Ngstate)


@app.create(bare=True)
def create() -> pt.Expr:
    return app.initialize_global_state()


@app.opt_in(bare=True)
def opt_in() -> pt.Expr:
    return pt.Seq(
        pt.If(app.state.prvi_igrac.get() == pt.Bytes("Bez igraca"))
        .Then(app.state.prvi_igrac.set(pt.Txn.sender()))
        .ElseIf(app.state.drugi_igrac.get() == pt.Bytes("Bez igraca"))
        .Then(app.state.drugi_igrac.set(pt.Txn.sender()))
        .Else(pt.Reject()),
        app.initialize_local_state(addr=pt.Txn.sender()),
    )


# pocetak igre, zapocinje prvi igrac i zadaje broj
@app.external(authorize=beaker.Authorize.opted_in())
def pocetak_igre(
    payment: pt.abi.PaymentTransaction, number: pt.abi.String, *, output: pt.abi.String
) -> pt.Expr:
    return pt.Seq(
        pt.Assert(
            pt.And(
                payment.type_spec().txn_type_enum() == pt.TxnType.Payment,
                payment.get().receiver() == pt.Global.current_application_address(),
                app.state.betting_tip.get() == pt.Int(0),
                app.state.number[pt.Txn.sender()].get() == pt.Bytes("Bez broja"),
                app.state.hash_number[pt.Txn.sender()] == pt.Bytes("Bez hash broja"),
            )
        ),
        app.state.betting_tip.set(payment.get().amount()),
        app.state.hash_number[pt.Txn.sender()].set(pt.Sha256(number.get())),
        output.set("Uspesno sacuvan broj!"),
    )


@app.external
def hello(name: pt.abi.String, *, output: pt.abi.String) -> pt.Expr:
    return output.set(pt.Concat(pt.Bytes("Hello, "), name.get()))
