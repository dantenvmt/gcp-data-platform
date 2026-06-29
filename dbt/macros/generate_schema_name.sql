{#
  By default dbt builds models into a schema like `<target>_<custom>`.
  This override makes dbt use the custom schema name verbatim, so our
  `+schema: staging` / `+schema: marts` map directly to the `staging`
  and `marts` BigQuery datasets we created in Terraform.
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
