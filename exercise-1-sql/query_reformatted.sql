select distinct dp.dir_uid as username, de.mail as email,
        case
            when dp.primaryaffiliation = 'Student' then 'Student'
            when dp.primaryaffiliation = 'Faculty' then
              case
                when daf.edupersonaffiliation = 'Faculty'and daf.description = 'Student Faculty' then 'Student'
                else 'Faculty/Staff'
              end
            when dp.primaryaffiliation = 'Staff' then 'Faculty/Staff'
            when dp.primaryaffiliation = 'Employee' then
              case
                when daf.edupersonaffiliation = 'Employee' and daf.description = 'Student Employee' then 'Student'
                when daf.edupersonaffiliation = 'Employee' and daf.description = 'Student Faculty' then 'Student'
                else 'Faculty/Staff'
              end
            when dp.primaryaffiliation = 'Officer/Professional' then 'Faculty/Staff'
            when dp.primaryaffiliation = 'Affiliate' and daf.edupersonaffiliation = 'Affiliate' and daf.description = 'Student Employee' then 'Student'
            when dp.primaryaffiliation = 'Affiliate' and daf.edupersonaffiliation = 'Affiliate' and daf.description = 'Continuing Ed Non-Credit Student' then 'Student'
            when dp.primaryaffiliation = 'Member' and daf.edupersonaffiliation = 'Member' and daf.description = 'Faculty' then 'Faculty/Staff'
            else 'Student'
        end
        as person_type
    from dirsvcs.dir_person dp inner join dirsvcs.dir_affiliation daf on daf.uuid = dp.uuid
        and daf.campus = 'Boulder Campus'
        and dp.primaryaffiliation not in ('Not currently affiliated', 'Retiree', 'Affiliate', 'Member')
        and daf.description not in ('Admitted Student', 'Alum', 'Confirmed Student', 'Former Student', 'Member Spouse',
            'Sponsored', 'Sponsored EFL', 'Retiree', 'Boulder3')
        and daf.description not like 'POI_%'
    left join dirsvcs.dir_email de on de.uuid = dp.uuid
        and de.mail_flag = 'M'
        and de.mail is not null
    where (
            dp.primaryaffiliation != 'Student'
            and lower(de.mail) not like '%cu.edu'
        )
        or (
            dp.primaryaffiliation = 'Student'
            and exists (
              select 'x' from dirsvcs.dir_acad_career where uuid = dp.uuid
        )
      )
      and de.mail is not NULL
      and lower(de.mail) not like '%cu.edu';
