from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from rentastay import definitions
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime

NULL = None

def getProperties():
    cursor = connection.cursor()
    query = """SELECT PROPERTY_ID, PROPERTY_NAME, COMUNA_NAME, REGION_NAME
            FROM PROPERTIES JOIN ADDRESSES USING(ADDRESS_ID) 
            JOIN COMUNAS USING(COMUNA_ID) 
            JOIN REGIONS USING(REGION_ID)"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    cursor.close()
    return result

def getYourProperties(request):
    cursor = connection.cursor()
    query = "SELECT USER_ID FROM USERS WHERE USERNAME=%s"
    if 'username' not in request.session:
        return redirect('home')
    cursor.execute(query,[request.session['username']])
    user_id = definitions.dictfetchone(cursor)
    if not bool(user_id):
        messages.error(request, 'Por favor, inicia sesión en tu cuenta.')
        cursor.close()
        return redirect('signin')
    user_id = user_id["USER_ID"]
    query = "SELECT PROPERTY_ID FROM PROPERTIES WHERE USER_ID=%s"
    cursor.execute(query,[str(user_id)])
    result1 = cursor.fetchall()
    result1 = [property_id[0] for property_id in result1]
    fetchedData = []
    for i in result1:
        query = """SELECT PROPERTY_ID, PROPERTY_NAME, COMUNA_NAME, REGION_NAME
            FROM PROPERTIES JOIN ADDRESSES USING(ADDRESS_ID) 
            JOIN COMUNAS USING(COMUNA_ID) 
            JOIN REGIONS USING(REGION_ID)
            WHERE PROPERTY_ID=%s"""
        cursor.execute(query,[str(i)])
        fetchedData.append(cursor.fetchone())
        columns = [col[0] for col in cursor.description]
    
    cursor.close()
    if len(fetchedData)==0:
        newlst=None
    else:
        newlst = [
            dict(zip(columns, row))
            for row in fetchedData
        ]
    return newlst

def home(request):
    properties = getProperties()
    data = {'properties': properties}
    return render(request, 'pages/home.html', data)

def yourproperties(request):
    properties = getYourProperties(request)
    data = {'properties': properties}
    return render(request, 'pages/yourproperties.html', data)

def getJsonPropertyData(request):
    properties = getProperties()
    return JsonResponse({'data':properties})

def getJsonYourPropertyData(request):
    properties = getYourProperties(request)
    return JsonResponse({'data':properties})

def getJsonPropertyPhotosPath(request, property_id):
    cursor = connection.cursor()
    query = """SELECT PATH
            FROM PROPERTY_PHOTOS_PATH
            WHERE PROPERTY_ID = %s;"""
    cursor.execute(query, [property_id])
    result = definitions.dictfetchall(cursor)
    
    return JsonResponse({'paths':result})

def getJsonPropertyPriceRange(request, property_id):
    cursor = connection.cursor()
    minPrice = cursor.callfunc('GET_MIN_PRICE', float, [property_id])
    maxPrice = cursor.callfunc('GET_MAX_PRICE', float, [property_id])

    return JsonResponse({'minPrice':minPrice, 'maxPrice':maxPrice})

def getJsonAvailableRoomsData(request, property_id, check_in, check_out, guests):
    cursor = connection.cursor()
    query = """SELECT * FROM ROOMS R
            WHERE PROPERTY_ID = %s
            AND ROOM_NO NOT IN (
                SELECT ROOM_NO FROM RENTS
                WHERE PROPERTY_ID = R.PROPERTY_ID
                AND ((TO_DATE(%s, 'DD-MON-YYYY') BETWEEN CHECKIN AND CHECKOUT)
                OR (TO_DATE(%s, 'DD-MON-YYYY') BETWEEN CHECKIN AND CHECKOUT)
                OR (CHECKIN BETWEEN TO_DATE(%s, 'DD-MON-YYYY') AND TO_DATE(%s, 'DD-MON-YYYY'))))
            AND MAX_CAPACITY >= %s"""
    cursor.execute(query, [property_id, check_in, check_out, check_in, check_out, guests])
    rooms = definitions.dictfetchall(cursor)
    rooms = sorted(rooms, key=lambda i: i['ROOM_NO'])

    return JsonResponse({'rooms': rooms})

def updateReview(request, rent_id, owner_rating, property_rating, owner_review, property_review):
    if request.session.has_key('username') is False:
        return redirect('/')

    dateFormat = '%d-%b-%Y'
    updateTime = datetime.now().strftime("%d%m%Y%H%M%S")

    cursor = connection.cursor()
    query = """UPDATE RENTS
            SET OWNER_RATING = %s,
            OWNER_REVIEW = %s,
            PROPERTY_RATING = %s,
            PROPERTY_REVIEW = %s,
            REVIEW_DATE = SYSDATE
            WHERE RENT_ID = %s"""
    message = ''
    try:
        cursor.execute(query, [owner_rating, owner_review, property_rating, property_review, rent_id])
        cursor.close()
        message = 'True'
        return JsonResponse({'message': message})
    except Exception as e:
        print(e)
        message = 'False'
        return JsonResponse({'message': message})

def property(request, property_id):
    cursor = connection.cursor()
    query = """SELECT * 
            FROM PROPERTIES JOIN USERS USING(USER_ID)
            JOIN ADDRESSES USING (ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            WHERE PROPERTY_ID = %s"""
    cursor.execute(query, [property_id])
    result = definitions.dictfetchone(cursor)

    propertyFeatures = result["FEATURES"]

    if((propertyFeatures is not None) and (propertyFeatures is not NULL)):
        propertyFeatures = propertyFeatures.split("\\")
        del propertyFeatures[-1]
        result.update({
            'PROPERTY_FEATURES': propertyFeatures
        })

    minPrice = cursor.callfunc('GET_MIN_PRICE', float, [property_id])
    maxPrice = cursor.callfunc('GET_MAX_PRICE', float, [property_id])

    result.update({
        'MIN_PRICE': minPrice,
        'MAX_PRICE': maxPrice
    })

    query = """SELECT PATH
            FROM PROPERTY_PHOTOS_PATH
            WHERE PROPERTY_ID = %s"""
    cursor.execute(query, [property_id])
    photosPath = definitions.dictfetchall(cursor)

    query = """SELECT TRUNC(AVG(PROPERTY_RATING), 2) AVG_PROPERTY_RATING, 
            COUNT(PROPERTY_RATING) TOTAL_PROPERTY_REVIEWS
            FROM RENTS
            WHERE PROPERTY_ID = %s AND CHECKOUT < SYSDATE"""
    cursor.execute(query, [property_id])
    reviews = definitions.dictfetchone(cursor)
    result.update(reviews)

    query = """SELECT FIRST_NAME, PROPERTY_RATING, PROPERTY_REVIEW, 
            PROFILE_PIC, REVIEW_DATE
            FROM RENTS JOIN USERS USING(USER_ID)
            WHERE PROPERTY_ID = %s AND CHECKOUT < SYSDATE AND PROPERTY_REVIEW IS NOT NULL;"""
    cursor.execute(query, [property_id])
    reviews = definitions.dictfetchall(cursor)

    query = """SELECT TRUNC(AVG(OWNER_RATING), 2) AVG_OWNER_RATING, COUNT(OWNER_RATING) TOTAL_OWNER_RATING
            FROM RENTS
            WHERE PROPERTY_ID IN (
            SELECT PROPERTY_ID
            FROM PROPERTIES
            WHERE USER_ID = (
            SELECT USER_ID
            FROM PROPERTIES
            WHERE PROPERTY_ID = %s AND CHECKOUT < SYSDATE
            ))"""
    cursor.execute(query, [property_id])
    ownerRating = definitions.dictfetchone(cursor)
    cursor.close()

    return render(request, 'pages/property.html', {'property':result, 'reviews': reviews, 'owner_rating':ownerRating, 'photos_url': photosPath})

def reservation(request, property_id, room_no, check_in, check_out, guests):
    if request.method == 'GET':
        dateFormat = '%d-%b-%Y'
        checkInDate = datetime.strptime(check_in, dateFormat)
        checkOutDate = datetime.strptime(check_out, dateFormat)
        noOfDays = (checkOutDate - checkInDate).days

        data = {
            'property_id': property_id, 
            'room_no': room_no, 
            'check_in': checkInDate.strftime(dateFormat), 
            'check_out': checkOutDate.strftime(dateFormat),
            'guests': guests
        }
        cursor = connection.cursor()

        if request.session.get('username') is not None:
            query = """SELECT USERNAME FROM USERS
                    JOIN PROPERTIES USING(USER_ID)
                    WHERE PROPERTY_ID = %s;"""
            cursor.execute(query, [property_id])
            propertyOwner = cursor.fetchone()[0]
            if propertyOwner == request.session['username']:
                messages.error(request, 'No puedes alquilar tu propia propiedad')
                return redirect('/property/' + str(property_id))

            query = """SELECT *
                    FROM USERS 
                    WHERE USERNAME = %s"""
            cursor.execute(query, [request.session['username']])
            result = definitions.dictfetchone(cursor)
            data.update(result)

        query = """SELECT REGION_NAME
                FROM REGIONS"""
        cursor.execute(query, [])
        result = definitions.dictfetchall(cursor)
        data.update({
            'regions': result
        })

        query = """SELECT PROPERTY_NAME, PATH
                FROM PROPERTIES JOIN PROPERTY_PHOTOS_PATH USING(PROPERTY_ID)
                WHERE PROPERTY_ID = %s"""
        cursor.execute(query, [property_id])
        result = definitions.dictfetchall(cursor)
        data.update({
            'property': result[0]
        })

        query = """SELECT PRICE, OFFER_PCT
                FROM ROOMS
                WHERE PROPERTY_ID = %s AND ROOM_NO = %s"""
        cursor.execute(query, [property_id, room_no])
        result = definitions.dictfetchone(cursor)
        pricePerNight = result['PRICE']
        offer = result['OFFER_PCT']
        data.update({
            'room': result
        })

        totalPrice = pricePerNight * noOfDays
        totalOffer = round(totalPrice * (offer / 100))
        data.update({
            'daysReserving': noOfDays,
            'totalPrice':  f"{totalPrice:,}",
            'totalOffer': f"{totalOffer:,}",
            'totalPriceWithOffer': f"{(totalPrice - totalOffer):,}"
        })
        cursor.close()
            
        return render(request, 'pages/reservation.html', data)

    elif request.method == 'POST':
        amount = request.POST['price']
        paymentMethod = request.POST.get(
            'paymentMethod', 'Tarjeta de crédito o débito')
        username = request.session['username']
        propertyId = request.POST['propertyid']
        roomno = request.POST['roomno']
        checkInDate = request.POST['checkin']
        checkOutDate = request.POST['checkout']
        guests = request.POST['guests']

        cursor = connection.cursor()

        isAvailable = cursor.callfunc('IS_ROOM_AVAILABLE', str, [property_id, room_no, checkInDate, checkOutDate, guests])

        if isAvailable == 'N':
            messages.error(request, 'Lo sentimos, esta habitación no está disponible para las fechas seleccionadas.')
            return redirect('/')

        query = """SELECT USER_ID FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, [username])
        userId = cursor.fetchone()[0]

        transactionTime = datetime.now().strftime("%d%m%Y%H%M%S")
        transactionId = str(userId) + '-' + str(propertyId) + '-' + str(roomno) + '-' + str(transactionTime)

        query = """INSERT INTO PAYMENTS VALUES(%s, SYSDATE, %s, %s)"""
        try:
            cursor.execute(query, [transactionId, amount, paymentMethod])

            query = """INSERT INTO RENTS(USER_ID, PROPERTY_ID, ROOM_NO, TRANSACTION_ID, CHECKIN, CHECKOUT)
                    VALUES(%s, %s, %s, %s, TO_DATE(%s, \'DD-Mon-YYYY\'), TO_DATE(%s, \'DD-Mon-YYYY\'))"""
            cursor.execute(query, [userId, propertyId, roomno, transactionId, checkInDate, checkOutDate])
            messages.success(request, "Tu reserva se ha realizado con éxito")
        except IntegrityError:
            messages.error(request, "Error del servidor.")
        
        return redirect('/myRents/')

def myRents(request):
    if request.session.has_key('username') is False:
        messages.error(request, "Debes iniciar sesión para ver tus alquileres")
        return redirect('/accounts/signin/')
    
    username = request.session.get('username')
    cursor = connection.cursor()

    query = """SELECT USER_ID 
            FROM USERS
            WHERE USERNAME = %s"""
    cursor.execute(query, [username])
    userId = cursor.fetchone()[0]

    query = """SELECT RENT_ID, PROPERTY_ID, PROPERTY_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            PROPERTY_NO, STREET, POST_CODE, COMUNA_NAME, REGION_NAME,
            USERNAME, FIRST_NAME, LAST_NAME, PROPERTY_RATING, PROPERTY_REVIEW, OWNER_RATING, OWNER_REVIEW
            FROM RENTS R
            JOIN PROPERTIES P USING(PROPERTY_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            JOIN USERS O ON (P.USER_ID = O.USER_ID)
            WHERE R.USER_ID = %s 
            AND CHECKOUT < SYSDATE;"""
    cursor.execute(query, [userId])
    olderRents = definitions.dictfetchall(cursor)

    query = """SELECT RENT_ID, PROPERTY_ID, PROPERTY_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            PROPERTY_NO, STREET, POST_CODE, COMUNA_NAME, REGION_NAME,
            USERNAME, FIRST_NAME, LAST_NAME, PROPERTY_RATING, PROPERTY_REVIEW, OWNER_RATING, OWNER_REVIEW
            FROM RENTS R
            JOIN PROPERTIES P USING(PROPERTY_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            JOIN USERS O ON (P.USER_ID = O.USER_ID)
            WHERE R.USER_ID = %s 
            AND SYSDATE BETWEEN CHECKIN AND CHECKOUT;"""
    cursor.execute(query, [userId])
    ongoingRents = definitions.dictfetchall(cursor)

    query = """SELECT RENT_ID, PROPERTY_ID, PROPERTY_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            PROPERTY_NO, STREET, POST_CODE, COMUNA_NAME, REGION_NAME,
            USERNAME, FIRST_NAME, LAST_NAME, PROPERTY_RATING, PROPERTY_REVIEW, OWNER_RATING, OWNER_REVIEW
            FROM RENTS R
            JOIN PROPERTIES P USING(PROPERTY_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            JOIN USERS O ON (P.USER_ID = O.USER_ID)
            WHERE R.USER_ID = %s 
            AND CHECKIN > SYSDATE;"""
    cursor.execute(query, [userId])
    upcomingRents = definitions.dictfetchall(cursor)

    cursor.close()

    if len(ongoingRents) == 0:
        ongoingRents = None
    if len(olderRents) == 0:
        olderRents = None
    if len(upcomingRents) == 0:
        upcomingRents = None

    data = {
        'older_rents': olderRents,
        'ongoing_rents': ongoingRents,
        'upcoming_rents': upcomingRents
    }

    return render(request, 'pages/myrents.html', data)

def myGuests(request):
    if request.session.has_key('username') is False:
        messages.error(request, "Debes iniciar sesión para ver tus huéspedes")
        return redirect('/accounts/signin/')
    
    username = request.session.get('username')
    cursor = connection.cursor()
    
    query = """SELECT USER_ID 
            FROM USERS
            WHERE USERNAME = %s"""
    cursor.execute(query, [username])
    userId = cursor.fetchone()[0]

    query = """SELECT INITCAP(PROPERTY_NAME) PROPERTY_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            PROPERTY_NO, STREET, POST_CODE, COMUNA_NAME, REGION_NAME,
            FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, JOIN_DATE, PROFILE_PIC
            FROM RENTS
            JOIN USERS USING(USER_ID)
            JOIN PROPERTIES USING(PROPERTY_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            WHERE PROPERTY_ID IN (
            SELECT PROPERTY_ID
            FROM PROPERTIES
            WHERE USER_ID = %s)
            AND SYSDATE BETWEEN CHECKIN AND CHECKOUT;"""
    cursor.execute(query, [userId])
    currentGuests = definitions.dictfetchall(cursor)

    query = """SELECT INITCAP(PROPERTY_NAME) PROPERTY_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            PROPERTY_NO, STREET, POST_CODE, COMUNA_NAME, REGION_NAME,
            FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, JOIN_DATE, PROFILE_PIC
            FROM RENTS
            JOIN USERS USING(USER_ID)
            JOIN PROPERTIES USING(PROPERTY_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            WHERE PROPERTY_ID IN (
            SELECT PROPERTY_ID
            FROM PROPERTIES
            WHERE USER_ID = %s)
            AND SYSDATE > CHECKOUT;"""
    cursor.execute(query, [userId])
    olderGuests = definitions.dictfetchall(cursor)

    query = """SELECT INITCAP(PROPERTY_NAME) PROPERTY_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            PROPERTY_NO, STREET, POST_CODE, COMUNA_NAME, REGION_NAME,
            FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, JOIN_DATE, PROFILE_PIC
            FROM RENTS
            JOIN USERS USING(USER_ID)
            JOIN PROPERTIES USING(PROPERTY_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN COMUNAS USING (COMUNA_ID)
            JOIN REGIONS USING (REGION_ID)
            WHERE PROPERTY_ID IN (
            SELECT PROPERTY_ID
            FROM PROPERTIES
            WHERE USER_ID = %s)
            AND SYSDATE < CHECKIN;"""
    cursor.execute(query, [userId])
    upcomingGuests = definitions.dictfetchall(cursor)
    cursor.close()

    if len(currentGuests) == 0:
        currentGuests = None
    if len(olderGuests) == 0:
        olderGuests = None
    if len(upcomingGuests) == 0:
        upcomingGuests = None

    data = {
        'older_guests': olderGuests,
        'current_guests': currentGuests,
        'upcoming_guests': upcomingGuests
    }

    return render(request, 'pages/myguests.html', data)