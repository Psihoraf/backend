from datetime import date



from src.Schemas.bookings import BookingAdd


async def test_add_bookings(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2020, month=9, day=1),
        date_to=date(year=2028, month=8, day=8),
        price = 100,
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()

    booking = await db.bookings.get_one_or_none(id = new_booking.id)
    assert booking

    new_date = date(year=2026, month=10, day=1)
    update_booking = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=new_date,
        date_to=date(year=2028, month=8, day=8),
        price=100,
    )

    changed_booking = await db.bookings.edit(update_booking, True, id= booking.id )
    await db.commit()
    assert changed_booking.date_from == new_date
    print(f"{changed_booking}")



