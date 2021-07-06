def end_session(session, register) -> None:
    session.add(register)
    session.commit()
