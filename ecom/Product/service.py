from ..models import Category, SimpleProduct, VariantProduct, VariantType, VariantsType, AttributeType
import itertools

async def check_if_category_exists(name: str):
    category = await Category.find_one(Category.name==name)
    return category

async def check_if_product_exists(id: str):
    product = await SimpleProduct.get(id)
    return product

def create_new_variants(attributes: AttributeType, start=0) -> VariantsType:
    keys = attributes.keys()
    if len(keys) == 0: 
        return {}
    values = [set(value) for value in attributes.values()]
    combinations = list(itertools.product(*values))
    variants = {}
    for index, combination in enumerate(combinations):
        variants[f"v{index+start}"] = VariantType(variant=None, attributes=dict(zip(keys, combination)), is_valid=False)
    return variants

def get_updated_attribute_and_variants(product: VariantProduct, attribute_name: str, new_props: list[str]) -> VariantsType:
    old_props = product.attributes[attribute_name]
    updated_variants = {}
    index = 0
    for value in product.variants.values():
        if value.attributes[attribute_name] not in new_props:
            continue
        updated_variants[f"v{index}"] = value
        index += 1
    added_props = set([prop for prop in new_props if prop not in old_props])
    old_attributes = product.attributes.copy()
    old_attributes[attribute_name] = added_props
    added_variants = create_new_variants(old_attributes, index)
    old_attributes[attribute_name] = new_props
    return {"variants": {**updated_variants, **added_variants}, "attributes": old_attributes}
