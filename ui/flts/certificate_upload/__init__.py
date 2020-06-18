from stdm.settings import current_profile
from stdm.data.configuration import entity_model


def certificate_model_factory():
    """
    :return: Returns the certificate and supporting document SQLAlchemy models.
    :rtype: tuple
    """
    # Get the current profile
    curr_profile = current_profile()
    if not curr_profile:
        return None
    # Certificate entity
    cert_entity = curr_profile.entity(
        'Certificate'
    )

    if not cert_entity:
        return None

    # Get the certificate and certificate doc model
    cert_model, cert_doc_model = entity_model(
        cert_entity,
        with_supporting_document=True
    )

    return cert_model, cert_doc_model
