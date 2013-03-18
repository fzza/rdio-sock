RdioFieldService
=====================================

.. automodule:: rdiosock.services.fields

    .. autoclass:: RdioFieldService
        :members:

        **Fields**

        .. py:attribute:: fields

            :class:`dict`

            Dictionary of current field values

        **Events**

        .. py:attribute:: on_changed

            :class:`rdiosock.utils.EventHook`

            Field changed event

            **Callback Parameters:** (field_name, field_value)
