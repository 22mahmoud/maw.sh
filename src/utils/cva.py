def cva(base: str, *, variants=None, default_variants=None):
    variants = variants or {}
    default_variants = default_variants or {}

    def resolve(props=None):
        props = props or {}
        resolved = [base]
        context = {**default_variants, **props}

        for key, values in variants.items():
            value = context.get(key)
            if value in values:
                resolved.append(values[value])

        return " ".join(filter(None, resolved))

    return resolve
