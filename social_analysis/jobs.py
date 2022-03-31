job_to_category={
    'project manager':"business",
    'programmatore':"technical",
    'altra professione tecnica':"technical",
    'sistemista/DBA':"technical",
    'data analyst / scientist':"data",
    'supporto tecnico':"support",
    'lavoratore dei servizi':"service",
    'business developer':"business",
    'ui/ux designer':"creative",
    'graphic designer':"creative",
    'specialista digital marketing':"business",
    'team leader / CTO':"business",
    'altra professione creativa':"creative",
    'analista software':"technical",
    'altro':"other",
    'specialista SEO/SEM':"creative",
    'cyber security':"technical",
    'tester/QA':"technical",
    'social media manager':"creative",
    'copywriter':"creative",
    'ricercatore':"data",
    'community manager':"business",
}

def map_job_to_job_category(job):
    return job_to_category[job]