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


app = beaker.Application("numberguess")


@app.external
def hello(name: pt.abi.String, *, output: pt.abi.String) -> pt.Expr:
    return output.set(pt.Concat(pt.Bytes("Hello, "), name.get()))
