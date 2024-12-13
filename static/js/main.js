function redirectTo(path, ...params) {
    if (params.length % 2 !== 0) return
    let url = new URL(location.protocol + location.host + path)

    for (let i = 0; i < params.length;) {
        const parName = params[i++]
        const parValue = params[i++]

        if (parName && parValue) {
            url.searchParams.set(parName, parValue)
        }
    }

    document.location.href = url.toString()
}