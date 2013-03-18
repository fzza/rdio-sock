RdioList
=====================================

.. automodule:: rdiosock.objects.collection

    .. autoclass:: RdioList

        .. begin-RdioList

        .. automethod:: parse_items

        **RdioCollection**
        *(Inherited)*

            .. py:attribute:: start

                :class:`int`

            .. py:attribute:: total

                :class:`int`

            .. py:attribute:: number_results

                :class:`int`

            .. py:attribute:: type

                :class:`str`

            .. py:attribute:: type_count

                :class:`dict`

            .. py:attribute:: items

                list of :class:`rdiosock.objects.base.RdioBaseItem`

            .. automethod:: parse_items

            .. automethod:: parse_count

        **RdioBaseItem**
        *(Inherited)*

        .. include:: /rdiosock/objects/base.rst
            :start-after: begin-RdioBaseItem
            :end-before: end-RdioBaseItem

        .. end-RdioList

RdioCollection
=====================================

.. autoclass:: RdioCollection

    .. begin-RdioCollection

    .. py:attribute:: start

        :class:`int`

    .. py:attribute:: total

        :class:`int`

    .. py:attribute:: number_results

        :class:`int`

    .. py:attribute:: type

        :class:`str`

    .. py:attribute:: type_count

        :class:`dict`

    .. py:attribute:: items

        list of :class:`rdiosock.objects.base.RdioBaseItem`

    .. automethod:: parse_items

    .. automethod:: parse_count

    **RdioBaseItem**
    *(Inherited)*

    .. include:: /rdiosock/objects/base.rst
        :start-after: begin-RdioBaseItem
        :end-before: end-RdioBaseItem

    .. end-RdioCollection